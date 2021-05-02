CREATE OR REPLACE PACKAGE METR_TO_IMP IS
    g_inch_in_cm CONSTANT NUMBER := 0.032808399;
    g_inch_in_ft CONSTANT NUMBER := 12;
    g_lb_in_kg CONSTANT NUMBER := 2.20462262;
    FUNCTION CM_TO_FT(p_cm IN NUMBER) RETURN VARCHAR2;
    FUNCTION KG_TO_LB(p_kg IN NUMBER) RETURN NUMBER;
END METR_TO_IMP;

CREATE OR REPLACE PACKAGE BODY METR_TO_IMP IS
    FUNCTION CM_TO_FT(p_cm IN NUMBER)
    RETURN VARCHAR2 IS
        v_height VARCHAR2(10);
        v_ft NUMBER;
        v_in NUMBER;
    BEGIN
        v_ft := TRUNC(p_cm * g_inch_in_cm, 0);
        v_in := ROUND((p_cm * g_inch_in_cm - v_ft) * g_inch_in_ft, 0);
        v_height := v_ft || '''' || v_in || '"';
        RETURN v_height;
    END CM_TO_FT;
    FUNCTION KG_TO_LB(p_kg IN NUMBER)
    RETURN NUMBER IS
        v_weight NUMBER;
    BEGIN
        v_weight := ROUND(p_kg * g_lb_in_kg, 1);
        RETURN v_weight;
    END KG_TO_LB;
END METR_TO_IMP;