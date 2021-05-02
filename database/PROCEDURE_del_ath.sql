create or replace PROCEDURE del_ath
  (p_id  athletes.id%TYPE)
IS
BEGIN
  EXECUTE IMMEDIATE 'DELETE FROM athletes WHERE id = :id' 
    USING p_id;
END;