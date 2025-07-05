from datetime import datetime, timedelta
from sqlalchemy import func
from database.models import Deal, User, Refund


def generate_daily_report(session):
    """Собирает статистику за последние 24 часа"""
    now = datetime.utcnow()
    yesterday = now - timedelta(days=1)

    total_users = session.query(User).count()
    active_users = session.query(User).filter(User.last_activity >= yesterday).count()
    new_users = session.query(User).filter(User.created_at >= yesterday).count()

    total_deals = session.query(Deal).count()
    completed_deals = session.query(Deal).filter(
        Deal.status == "completed", Deal.date >= yesterday
    ).count()

    daily_revenue = (
        session.query(func.sum(Deal.revenue))
        .filter(Deal.status == "completed", Deal.date >= yesterday)
        .scalar()
        or 0.0
    )

    refund_count = session.query(Refund).filter(
        Refund.deal_id.in_(
            [d.id for d in session.query(Deal.id).filter(Deal.date >= yesterday)]
        )
    ).count()

    referral_revenue = (
            session.query(func.sum(User.ref_revenue))
            .filter(User.last_activity >= yesterday)
            .scalar() or 0.0
    )

    return {
        "date": now.strftime("%Y-%m-%d %H:%M UTC"),
        "total_users": total_users,
        "active_users": active_users,
        "new_users": new_users,
        "total_deals": total_deals,
        "completed_deals": completed_deals,
        "daily_revenue": round(float(daily_revenue), 2),
        "refund_count": refund_count,
        "referral_revenue": round(float(referral_revenue), 2),
    }


def format_report(report_data):
    """Форматирует отчет в удобный текст"""
    text = f"📊 <b>Ежедневный отчет — {report_data['date']}</b>\n\n👥 Всего пользователей: {report_data['total_users']}\n<i>Активных за сутки: {report_data['active_users']}</i>\n<i>Новых за сутки: {report_data['new_users']}</i>\n\n🤝<b> Всего сделок: {report_data['total_deals']}</b>\nЗавершено за сутки: {report_data['completed_deals']}\nДоход за сутки: {report_data['daily_revenue']} TON\n\n🎁 Общие доходы рефералов: {report_data['referral_revenue']} TON\n"
    return text