module.exports = {
  apps: [
    {
      name: 'django',
      script: 'C:\\Users\\User\\AppData\\Local\\Programs\\Python\\Python313\\python.exe',
      args: 'manage.py runserver 127.0.0.1:8000',
      cwd: 'C:\\Users\\User\\Desktop\\jenkins\\tutor-ontrol_server',
      interpreter: 'none'
    },
    {
      name: "vue",
      cwd: "C:\\Users\\User\\Desktop\\jenkins\\tutor-ontrol_server\\client",
      script: "cmd",
      args: "/c npm run dev",
      interpreter: "none"
    }
  ]
};