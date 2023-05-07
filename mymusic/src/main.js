import { createApp } from 'vue'
import App from './App.vue'

import router from './router'

import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import zhCn from 'element-plus/es/locale/lang/zh-cn'

import '@/assets/css/globalCSS.css'

import * as ElementPlusIconsVue from '@element-plus/icons-vue'
const app = createApp(App);
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
    app.component(key, component)
}

createApp(App)
    .use(router)
    .use(ElementPlus, {locale: zhCn,})
    .mount('#app')