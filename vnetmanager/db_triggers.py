
def gettriggers():

    switchlink_triggers = [
        ('Verify_SwitchLink_ins', 'INSERT'),
        ('Verify_SwitchLink_up', 'UPDATE')
    ]

    switchlink_trigger_format = "\n".join([
        "CREATE TRIGGER %s BEFORE %s ON switch_link",
        "FOR EACH ROW",
        "BEGIN",
        "   DECLARE msg VARCHAR(255);",
        "    IF (NEW.dstswitch_id IS NOT NULL AND NEW.dsthost_id IS NOT NULL) OR",
        "    (NEW.dstswitch_id IS NULL AND NEW.dsthost_id IS NULL) THEN",
        "        SET msg = 'Destination constraint violated.';",
        "        SIGNAL sqlstate '45000' SET message_text = msg;",
        "    END IF;",
        "END;"
    ])

    return { t[0]: switchlink_trigger_format % t for t in switchlink_triggers }


