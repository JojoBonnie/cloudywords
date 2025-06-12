@echo off
echo Running all tests...

echo.
echo ===== BACKEND TESTS =====
echo.
call run_backend_tests.bat

echo.
echo ===== FRONTEND TESTS =====
echo.
call run_frontend_tests.bat

echo.
echo All tests completed.