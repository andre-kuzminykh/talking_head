"""
Router registration for the bot.
"""
from core.loader import dp
from handler.v1.user.router import user_router
from handler.v1.user.welcome.F001.start_widget import welcome_router
from handler.v1.user.photo.F002.upload_photo_widget import upload_photo_router
from handler.v1.user.photo.F004.select_photo_widget import select_photo_router
from handler.v1.user.text.F005.text_input_widget import text_input_router

# Register sub-routers into user_router
user_router.include_router(welcome_router)
user_router.include_router(upload_photo_router)
user_router.include_router(select_photo_router)
user_router.include_router(text_input_router)

# Register user_router into dispatcher
dp.include_router(user_router)
