CREATE OR REPLACE PACKAGE pac_cur AS 
    PROCEDURE event_con (p_season athletes.season%TYPE, p_city athletes.city%TYPE);
    PROCEDURE cur_query (p_age athletes.age%TYPE, p_year athletes.year%TYPE);
END pac_cur;
 
CREATE OR REPLACE PACKAGE BODY pac_cur IS
    PROCEDURE event_con (p_season athletes.season%TYPE, p_city athletes.city%TYPE) IS
        cv SYS_REFCURSOR;
        ye athletes.year%TYPE;
        ev athletes.event%TYPE;
        p_st  VARCHAR2(100);
    BEGIN
        p_st := 'SELECT year,event FROM athletes WHERE ' ||
                'season = :sea AND city = :cit';
        OPEN cv FOR p_st USING p_season, p_city;
            DBMS_OUTPUT.PUT_LINE('Year    Event');
            DBMS_OUTPUT.PUT_LINE('-----    -------');
            LOOP
                FETCH cv INTO ye, ev;
                EXIT WHEN cv%NOTFOUND;
                DBMS_OUTPUT.PUT_LINE(ye || '     ' || ev);
            END LOOP;
        CLOSE cv;
    END event_con;
    
    PROCEDURE cur_query (p_age athletes.age%TYPE, p_year athletes.year%TYPE) IS
        c_refcur SYS_REFCURSOR;
        v_name athletes.name%TYPE;
        v_tname athletes.team%TYPE;
        p_string VARCHAR2(100);
    BEGIN
        p_string := 'SELECT name, team FROM athletes WHERE ' ||
                    'age = :age AND year = :year';
        OPEN c_refcur FOR p_string USING p_age, p_year;
            DBMS_OUTPUT.PUT_LINE('Athlete     Team');
            DBMS_OUTPUT.PUT_LINE('-----    ------');
            LOOP
                FETCH c_refcur INTO v_name, v_tname;
                EXIT WHEN c_refcur%NOTFOUND;
                DBMS_OUTPUT.PUT_LINE(v_name || '     ' || v_tname);
            END LOOP;
        CLOSE c_refcur;
    END cur_query;
END pac_cur;
