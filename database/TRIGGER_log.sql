create or replace trigger log_create_table_trigg
after create on schema
begin 
    if sys.DICTIONARY_OBJ_TYPE = 'TABLE' and DICTIONARY_OBJ_name not like '%LOG%' THEN
        dev_package.create_log_table(DICTIONARY_OBJ_name);
    end if;
end;