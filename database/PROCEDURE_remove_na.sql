CREATE OR REPLACE PROCEDURE REMOVE_NA (p_table IN VARCHAR2) IS
    TYPE t_cols IS TABLE OF USER_TAB_COLUMNS%ROWTYPE INDEX BY BINARY_INTEGER;
    v_colstab t_cols;
    v_update_query VARCHAR2(20) := 'UPDATE ' || p_table;
    v_query VARCHAR2(100);
BEGIN
    SELECT * BULK COLLECT INTO v_colstab
    FROM USER_TAB_COLUMNS
    WHERE table_name = p_table;
    FOR i IN v_colstab.FIRST..v_colstab.LAST LOOP
        IF v_colstab.EXISTS(i) AND v_colstab(i).data_type = 'VARCHAR2' AND v_colstab(i).nullable = 'Y' THEN
        v_query := v_update_query || ' ' ||
            'SET ' || v_colstab(i).column_name || ' = NULL '
            || 'WHERE ' || v_colstab(i).column_name || ' = ''NA''';
        EXECUTE IMMEDIATE v_query;
        DBMS_OUTPUT.PUT_LINE(SQL%ROWCOUNT || ' rows updated');
        END IF;
        v_query := '';
    END LOOP;
END;

BEGIN
    REMOVE_NA('ATHLETES_TEMP');
END;