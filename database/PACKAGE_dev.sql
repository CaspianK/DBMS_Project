CREATE OR REPLACE PACKAGE dev_package IS
    PROCEDURE REMOVE_NA (p_table IN VARCHAR2);
    procedure create_log_table(p_table_name varchar);
END dev_package;