import { createApp } from 'vue'
import router from '@/router'
import App from './App.vue'
import pinia from '@/store'
import './style.css'

createApp(App)
    .use(router)
    .use(pinia)
    .mount('#app')
