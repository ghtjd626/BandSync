import pandas as pd
from datetime import datetime, timedelta
from itertools import product

class BandScheduler:
    def __init__(self):
        self.members = pd.DataFrame()

    def add_member(self, name, location, availability):
        """
        밴드 멤버를 위치와 주간 가능 시간과 함께 추가합니다.
        :param name: 멤버의 이름
        :param location: 멤버의 위치 (예: NY, LA)
        :param availability: 가능한 시간대 목록 (예: ["Mon 10:00-12:00", "Wed 14:00-16:00"])
        """
        self.members = pd.concat([self.members, pd.DataFrame([{
            'name': name,
            'location': location,
            'availability': availability
        }])], ignore_index=True)

    def find_schedule(self, location=None):
        """
        밴드 연습을 위한 최적의 스케줄을 제안합니다.
        :param location: 스케줄링을 위한 선택적 위치 필터.
        :return: 최대 참석 인원을 가진 제안된 스케줄.
        """
        # 위치가 지정된 경우 멤버를 위치로 필터링
        members = self.members
        if location:
            members = members[members['location'] == location]

        # 모든 가능 시간대 수집
        all_slots = []
        for _, member in members.iterrows():
            for slot in member['availability']:
                day, times = slot.split()
                start, end = times.split('-')
                all_slots.append({
                    'name': member['name'],
                    'day': day,
                    'start': datetime.strptime(start, "%H:%M"),
                    'end': datetime.strptime(end, "%H:%M")
                })

        # 가능한 시간대 생성
        time_slots = self._generate_time_slots(all_slots)

        # 각 시간대에 대한 참석 인원 평가
        attendance = self._evaluate_attendance(time_slots, all_slots)

        # 가장 좋은 시간대 반환
        return sorted(attendance, key=lambda x: -x['attendees'])

    def _generate_time_slots(self, all_slots):
        """
        주어진 가능 시간대로부터 가능한 시간대를 생성합니다.
        """
        days = set(slot['day'] for slot in all_slots)
        times = [datetime.strptime("08:00", "%H:%M") + timedelta(minutes=30 * i) for i in range(20)]
        return [{'day': day, 'start': t, 'end': t + timedelta(hours=1)} for day, t in product(days, times)]

    def _evaluate_attendance(self, time_slots, all_slots):
        """
        각 시간대에 몇 명의 멤버가 참석할 수 있는지 평가합니다.
        """
        results = []
        for slot in time_slots:
            attendees = 0
            for member_slot in all_slots:
                if member_slot['day'] == slot['day'] and \
                   member_slot['start'] <= slot['start'] and \
                   member_slot['end'] >= slot['end']:
                    attendees += 1
            results.append({**slot, 'attendees': attendees})
        return results

# 예제 사용법
if __name__ == "__main__":
    scheduler = BandScheduler()
    scheduler.add_member("앨리스", "NY", ["Mon 10:00-12:00", "Wed 14:00-16:00"])
    scheduler.add_member("밥", "NY", ["Mon 11:00-13:00", "Wed 15:00-17:00"])
    scheduler.add_member("찰리", "NY", ["Mon 10:30-12:30", "Wed 14:00-16:30"])

    suggested_schedule = scheduler.find_schedule(location="NY")
    for slot in suggested_schedule[:5]:  # 상위 5개 슬롯 표시
        print(f"날짜: {slot['day']}, 시작: {slot['start'].strftime('%H:%M')}, 종료: {slot['end'].strftime('%H:%M')}, 참석자 수: {slot['attendees']}")
