

from sqlalchemy import DDL, event
from .message import Message

create_fn_sql = DDL("""
CREATE OR REPLACE FUNCTION touch_conversation_last_message()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE conversations
    SET last_message_at = NEW.created_at
    WHERE id = NEW.conversation_id;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
""")

create_trg_sql = DDL("""
CREATE TRIGGER trg_touch_conversation_last_message
AFTER INSERT ON messages
FOR EACH ROW
EXECUTE FUNCTION touch_conversation_last_message();
""")


event.listen(
    Message.__table__, 
    "after_create", 
    create_fn_sql.execute_if(dialect="postgresql")
)
event.listen(
    Message.__table__, 
    "after_create", 
    create_trg_sql.execute_if(dialect="postgresql")
)