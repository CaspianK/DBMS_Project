CREATE OR REPLACE PROCEDURE POPULATE_SPORTS IS
    v_src BFILE;
    v_dest BLOB;
    v_name VARCHAR2(50);
    CURSOR c_sports IS
        SELECT SPORT FROM SPORTS ORDER BY SPORT;
BEGIN
    FOR v_rec IN c_sports LOOP
        v_name := v_rec.sport || '.jpg';
        v_src := BFILENAME('SPORTS_IMAGES', v_name);
        UPDATE SPORTS SET IMAGE = EMPTY_BLOB() WHERE SPORT = v_rec.sport 
                RETURNING image INTO v_dest;
        DBMS_LOB.OPEN(v_src, DBMS_LOB.LOB_READONLY);
        DBMS_LOB.LoadFromFile(  DEST_LOB => v_dest,
                                SRC_LOB => v_src,
                                AMOUNT => DBMS_LOB.GETLENGTH(v_src));
        DBMS_LOB.CLOSE(v_src);
    END LOOP;
END;
    