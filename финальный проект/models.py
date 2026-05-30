from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


db = SQLAlchemy()

class EnergySurvey(db.Model):
    __tablename__ = 'energy_survey'

    id = db.Column(db.Integer, primary_key=True)
    total_kwh_per_month = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    @classmethod
    def get_average_kwh(cls):
        result = db.session.query(db.func.avg(cls.total_kwh_per_month)).scalar()
        return round(result,2)
    
    def compare_with_average(self):
        avg = self.get_average_kwh()
        if avg == 0:
            return {
                'current_kwh': self.total_kwh_per_month,
                'average_kwh': 0,
                'difference': 0,
                'message': 'Нет данных для сравнения',
            }

        difference = self.total_kwh_per_month - avg
        return {
            'current_kwh': self.total_kwh_per_month,
            'average_kwh': avg,
            'difference': round(difference, 2),
            'percent': round((difference / avg) * 100, 2),
            'message': 'выше среднего' if difference > 0 else 'ниже среднего' if difference < 0 else 'равен среднему',
        }
