CREATE OR REPLACE PACKAGE pac_sex AS
    TYPE t_ath IS TABLE OF ATHLETES%ROWTYPE INDEX BY BINARY_INTEGER;
    FUNCTION man_ath (p_team VARCHAR2) RETURN t_ath;
    FUNCTION woman_ath (p_team VARCHAR2) RETURN t_ath;
END pac_sex;
 
CREATE OR REPLACE PACKAGE BODY pac_sex AS
    FUNCTION man_ath (p_team VARCHAR2) RETURN t_ath IS
        v_ath t_ath;
    BEGIN
        SELECT * BULK COLLECT INTO v_ath FROM athletes
        WHERE SEX = 'M' AND team = p_team
        ORDER BY year;
        RETURN v_ath;
    END man_ath;
    
    FUNCTION woman_ath (p_team VARCHAR2) RETURN t_ath IS
        v_ath t_ath;
    BEGIN
        SELECT * BULK COLLECT INTO v_ath FROM athletes
        WHERE SEX = 'F' AND team = p_team
        ORDER BY year;
        RETURN v_ath;
    END woman_ath;
END pac_sex;