CREATE OR REPLACE FUNCTION CALCULATE_BMI(p_weight IN NUMBER, p_height IN NUMBER)
RETURN NUMBER IS
    v_bmi NUMBER;
BEGIN
    v_bmi := ROUND(p_weight / POWER((p_height / 100), 2), 1);
    RETURN v_bmi;
END;