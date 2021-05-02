create or replace procedure create_log_table(p_table_name varchar) IS
var2 varchar2(10000);
var1 varchar2(4000) := 'id number, OPERATION_DATE DATE, ACTION VARCHAR(255), ACTIONAUTHOR VARCHAR(255)';
var3 varchar2(4000) := 'id, OPERATION_DATE, ACTION, ACTIONAUTHOR';
var4 varchar2(4000) := 'new_id, sysdate';
var5 varchar2(4000);
CURSOR cur_table is
    select column_name,data_type
    from user_tab_columns
    where table_name = p_table_name;
begin
    for i IN cur_table loop
        var1 := var1 ||', '||'old_'||i.column_name ||' '||i.data_type||', '||'new_'||i.column_name|| ' ' ||i.data_type;
        var3 := var3 ||', '||'old_'||i.column_name ||', '||'new_'||i.column_name;
        var5 := var5 ||', '||':old.'||i.column_name ||', '||':new.'||i.column_name;
    end loop;
    EXECUTE IMMEDIATE 'create table ' || p_table_name || '_LOG' || '(' || REPLACE(var1, 'VARCHAR2', 'VARCHAR(255)') || ')'; 
     var2 := 'create or replace trigger ' || p_table_name ||'_trig  
    AFTER DELETE OR INSERT OR UPDATE on '|| p_table_name ||' FOR EACH ROW
    declare
        new_id number;
    BEGIN
        IF DELETING THEN
            select NVL(MAX(id), 0)+1 into new_id from ' || p_table_name || '_LOG;
            INSERT INTO ' || p_table_name || '_log('||var3||')
            VALUES('||var4||',''delete'',user'||var5||');
        END IF; 
        IF INSERTING THEN
            select NVL(MAX(id), 0)+1 into new_id from ' || p_table_name || '_LOG;
            INSERT INTO ' || p_table_name || '_log('||var3||')
            VALUES('||var4||',''insert'',user'||var5||');
        END IF;
        IF UPDATING THEN
            select NVL(MAX(id), 0)+1 into new_id from ' || p_table_name || '_LOG;
            INSERT INTO ' || p_table_name || '_log('||var3||')
            VALUES('||var4||',''update'',user'||var5||');
        END IF;
    END;';
    EXECUTE IMMEDIATE var2;
end;