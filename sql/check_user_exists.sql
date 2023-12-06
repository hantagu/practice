SELECT EXISTS (
    SELECT True FROM "users" WHERE "login" = %s
)
