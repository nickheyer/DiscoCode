
async def requires_admin(cls):
  if not cls.user_config.is_admin:
    return True
  return False