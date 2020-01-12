# import os
#
# import pkg_resources
# from paste.deploy import appconfig
# from sqlalchemy import engine_from_config
# from sqlalchemy.orm import scoped_session
# from sqlalchemy.orm import sessionmaker
#
# location = pkg_resources.get_distribution('airgql').location
# config = appconfig(f'config:{os.path.join(location, "development.ini")}',
#                    'main')
#
# engine = engine_from_config(config, 'sqlalchemy.')
# db_session = scoped_session(
#     sessionmaker(autocommit=False, autoflush=False, bind=engine)
# )
