TEXTS = {
    "ru": {
        "choose_language": "Выберите язык.",
        "language_saved": "Язык сохранён: Русский. Теперь отправьте вашу проблему одним сообщением.",
        "send_issue": "Отправьте вашу проблему одним сообщением. Новые сообщения до закрытия заявки будут заблокированы.",
        "ticket_created": "Ваша заявка #{ticket_id} создана. Сотрудник поддержки скоро свяжется с вами.",
        "ticket_already_exists": "У вас уже есть активная заявка #{ticket_id}. Дождитесь ответа или закрытия заявки.",
        "assigned_user_no_username": "по имени {admin_name}",
        "assigned_user_with_username": "сотрудником {admin_name} (@{admin_username})",
        "ticket_claimed_user": "Ваша заявка #{ticket_id} принята {admin_display}. Писать вам будет только этот сотрудник. Если напишет кто-то другой, это не наша поддержка.",
        "ticket_closed_user": "Ваша заявка #{ticket_id} закрыта.",
        "language_not_selected": "Сначала выберите язык.",
        "unsupported_message": "Поддерживаются только текстовые сообщения.",
    },
    "en": {
        "choose_language": "Choose your language.",
        "language_saved": "Language saved: English. Now send your issue in one message.",
        "send_issue": "Send your issue in one message. New messages will be blocked until the ticket is closed.",
        "ticket_created": "Your ticket #{ticket_id} has been created. A support agent will contact you soon.",
        "ticket_already_exists": "You already have an active ticket #{ticket_id}. Please wait for a reply or ticket closure.",
        "assigned_user_no_username": "by {admin_name}",
        "assigned_user_with_username": "by {admin_name} (@{admin_username})",
        "ticket_claimed_user": "Your ticket #{ticket_id} has been accepted {admin_display}. Only this staff member will contact you. If someone else writes to you, it is not our support.",
        "ticket_closed_user": "Your ticket #{ticket_id} has been closed.",
        "language_not_selected": "Choose a language first.",
        "unsupported_message": "Only text messages are supported.",
    },
    "es": {
        "choose_language": "Elige tu idioma.",
        "language_saved": "Idioma guardado: Español. Ahora envía tu problema en un solo mensaje.",
        "send_issue": "Envía tu problema en un solo mensaje. Los nuevos mensajes estarán bloqueados hasta que se cierre el ticket.",
        "ticket_created": "Tu ticket #{ticket_id} ha sido creado. Un agente de soporte te contactará pronto.",
        "ticket_already_exists": "Ya tienes un ticket activo #{ticket_id}. Espera una respuesta o el cierre del ticket.",
        "assigned_user_no_username": "por {admin_name}",
        "assigned_user_with_username": "por {admin_name} (@{admin_username})",
        "ticket_claimed_user": "Tu ticket #{ticket_id} ha sido aceptado {admin_display}. Solo esta persona de soporte te escribirá. Si te escribe alguien más, no es nuestro soporte.",
        "ticket_closed_user": "Tu ticket #{ticket_id} ha sido cerrado.",
        "language_not_selected": "Primero elige un idioma.",
        "unsupported_message": "Solo se admiten mensajes de texto.",
    },
}


SUPPORTED_LANGUAGES = {"ru", "en", "es"}



def t(language: str, key: str, **kwargs) -> str:
    data = TEXTS.get(language, TEXTS["en"])
    template = data[key]
    return template.format(**kwargs)
