from fastapi_jwt_auth import AuthJWT
from database.config import jwtsettings

authjwt_secret_key = jwtsettings.JWT_SECRET_KEY
authjwt_algorithm = jwtsettings.JWT_ALGORITHM

authjwt = AuthJWT()
# authjwt.secret_key = jwtsettings.JWT_SECRET_KEY
# authjwt.algorithm = jwtsettings.JWT_ALGORITHM

authjwt.authjwt_secret_key = jwtsettings.JWT_SECRET_KEY
authjwt.authjwt_decode_algorithm = jwtsettings.JWT_ALGORITHM
