from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import or_
import os, json

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bandsync.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# 데이터베이스 모델
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    user_type = db.Column(db.String(20))  # 'musician' or 'band'
    
    # 뮤지션 프로필
    instrument = db.Column(db.String(50))
    genre = db.Column(db.String(100))
    skill_level = db.Column(db.String(20))
    location = db.Column(db.String(100))
    age = db.Column(db.Integer)
    bio = db.Column(db.Text)

    # 밴드 추가 정보
    recruiting_positions = db.Column(db.Text)  # JSON 형식으로 저장: [{"instrument": "guitar", "skill_level": "intermediate"}]
    band_size = db.Column(db.Integer)  # 현재 밴드 인원
    preferred_age_range = db.Column(db.String(50))  # "20-30"과 같은 형식

    def get_recruiting_positions(self):
        if self.recruiting_positions:
            return json.loads(self.recruiting_positions)
        return []

    def set_recruiting_positions(self, positions):
        self.recruiting_positions = json.dumps(positions)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search')
def search():
    # 검색 매개변수 가져오기
    instrument = request.args.get('instrument')
    genre = request.args.get('genre')
    location = request.args.get('location')
    user_type = request.args.get('user_type')
    skill_level = request.args.get('skill_level')

    # 기본 쿼리 생성
    query = User.query

    # 검색 조건 적용
    if user_type:
        query = query.filter(User.user_type == user_type)
    if instrument:
        query = query.filter(User.instrument == instrument)
    if genre:
        query = query.filter(User.genre == genre)
    if location:
        query = query.filter(User.location == location)
    if skill_level:
        query = query.filter(User.skill_level == skill_level)

    # 현재 로그인한 사용자 제외
    if current_user.is_authenticated:
        query = query.filter(User.id != current_user.id)

    # 결과 가져오기
    results = query.all()

    return render_template('search_results.html', results=results)

@app.route('/recommendations')
@login_required
def get_recommendations():
    # 현재 사용자와 반대되는 user_type 설정
    target_type = 'musician' if current_user.user_type == 'band' else 'band'
    
    # 기본 쿼리 생성
    query = User.query.filter(User.user_type == target_type)
    
    # 현재 사용자 제외
    query = query.filter(User.id != current_user.id)
    
    # 매칭 점수를 계산하여 결과 정렬
    results = []
    all_users = query.all()
    
    for user in all_users:
        score = 0
        
        # 장르 매칭
        if user.genre and current_user.genre and user.genre == current_user.genre:
            score += 3
            
        # 지역 매칭
        if user.location and current_user.location and user.location == current_user.location:
            score += 2
            
        # 실력 수준 매칭
        if user.skill_level and current_user.skill_level:
            skill_levels = ['beginner', 'intermediate', 'advanced', 'professional']
            user_skill_idx = skill_levels.index(user.skill_level)
            current_skill_idx = skill_levels.index(current_user.skill_level)
            if abs(user_skill_idx - current_skill_idx) <= 1:  # 실력 차이가 1단계 이내
                score += 1
        
        if score > 0:  # 최소한 하나의 조건이라도 만족하는 경우만 추가
            results.append((user, score))
    
    # 점수에 따라 정렬
    results.sort(key=lambda x: x[1], reverse=True)
    
    # 상위 5개 결과만 반환
    top_recommendations = [r[0] for r in results[:5]]
    
    return top_recommendations

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    if request.method == 'POST':
        # 기본 정보 업데이트
        instrument = request.form.get('instrument')
        genre = request.form.get('genre')
        location = request.form.get('location')
        skill_level = request.form.get('skill_level')
        age = request.form.get('age')
        bio = request.form.get('bio')

        try:
            # 현재 사용자 정보 업데이트
            current_user.genre = genre
            current_user.location = location
            current_user.age = int(age) if age else None
            current_user.bio = bio

            # 밴드 타입일 경우 추가 정보 업데이트
            if current_user.user_type == 'band':
                band_size = request.form.get('band_size')
                preferred_age_range = request.form.get('preferred_age_range')
                current_user.band_size = int(band_size) if band_size else None
                current_user.preferred_age_range = preferred_age_range

                # 모집 포지션 정보 처리
                positions = []
                instruments = request.form.getlist('recruiting_instrument[]')
                skill_levels = request.form.getlist('recruiting_skill_level[]')
                
                for i in range(len(instruments)):
                    if instruments[i]:  # 빈 값이 아닌 경우만 추가
                        positions.append({
                            'instrument': instruments[i],
                            'skill_level': skill_levels[i] if i < len(skill_levels) else 'intermediate'
                        })
                
                current_user.set_recruiting_positions(positions)
            else:
                # 뮤지션 타입일 경우
                current_user.instrument = instrument
                current_user.skill_level = skill_level

            db.session.commit()
            flash('프로필이 성공적으로 업데이트되었습니다.', 'success')
            return redirect(url_for('dashboard'))
        except Exception as e:
            db.session.rollback()
            flash('프로필 업데이트 중 오류가 발생했습니다.', 'error')
            print(e)  # 디버깅용

    return render_template('edit_profile.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        user_type = request.form.get('user_type')

        # 유효성 검사
        if not all([username, email, password, confirm_password, user_type]):
            flash('모든 필드를 입력해주세요.', 'error')
            return redirect(url_for('register'))

        if password != confirm_password:
            flash('비밀번호가 일치하지 않습니다.', 'error')
            return redirect(url_for('register'))

        if User.query.filter_by(username=username).first():
            flash('이미 사용 중인 사용자 이름입니다.', 'error')
            return redirect(url_for('register'))

        if User.query.filter_by(email=email).first():
            flash('이미 사용 중인 이메일입니다.', 'error')
            return redirect(url_for('register'))

        user = User(
            username=username,
            email=email,
            user_type=user_type
        )
        user.password_hash = generate_password_hash(password)

        try:
            db.session.add(user)
            db.session.commit()
            flash('회원가입이 완료되었습니다!', 'success')
            return redirect(url_for('login'))
        except:
            db.session.rollback()
            flash('회원가입 중 오류가 발생했습니다.', 'error')
            return redirect(url_for('register'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            flash('사용자 이름과 비밀번호를 모두 입력해주세요.', 'error')
            return redirect(url_for('login'))

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            flash('로그인되었습니다!', 'success')
            return redirect(url_for('dashboard'))

        flash('잘못된 사용자 이름 또는 비밀번호입니다.', 'error')

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('로그아웃되었습니다.', 'success')
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    # 추천 결과 가져오기
    recommendations = get_recommendations()
    return render_template('dashboard.html', recommendations=recommendations)

def init_db():
    with app.app_context():
        # 데이터베이스 테이블 생성
        db.drop_all()  # 기존 테이블 삭제
        db.create_all()  # 새로운 테이블 생성
        
        # 테스트용 데이터 생성 (선택사항)
        test_band = User(
            username='test_band',
            email='band@test.com',
            user_type='band',
            genre='rock',
            location='seoul',
            bio='테스트 밴드입니다.',
            band_size=3,
            preferred_age_range='20-30'
        )
        test_band.password_hash = generate_password_hash('password')
        test_band.set_recruiting_positions([
            {'instrument': 'guitar', 'skill_level': 'intermediate'},
            {'instrument': 'drums', 'skill_level': 'advanced'}
        ])

        test_musician = User(
            username='test_musician',
            email='musician@test.com',
            user_type='musician',
            instrument='guitar',
            genre='rock',
            skill_level='intermediate',
            location='seoul',
            age=25,
            bio='테스트 뮤지션입니다.'
        )
        test_musician.password_hash = generate_password_hash('password')

        db.session.add(test_band)
        db.session.add(test_musician)
        db.session.commit()

if __name__ == '__main__':
    init_db()  # 데이터베이스 초기화
    app.run(debug=True) 