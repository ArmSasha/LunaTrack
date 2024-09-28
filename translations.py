translations = {
	'en': {
		'Успещная регистрация!': 'Seccessful registration!',
		'Добро пожаловать!': 'Welcome!',
		'Профиль': 'Profile',
		'Настройки': 'Settings',
	}
}

def trans(text, lang='ru'):
	if lang == 'ru':
		return text
	else:
		global translations
		try:
			return translations[lang][text]
		except:
			return translations