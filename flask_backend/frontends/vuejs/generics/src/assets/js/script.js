// assets/js/script.js
export default {
    name: 'HelloWorld',
    props: {
      msg: String
    },

        mounted() {
          document.getElementById('clickMeBtn').addEventListener('click', function() {
            alert('Hello from AppFizzle!');
          });
        }
      
  }