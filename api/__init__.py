try:
	import pymysql  # type: ignore

	pymysql.install_as_MySQLdb()
except Exception:
	# PyMySQL not available in some environments; ignore to allow tooling
	pass

