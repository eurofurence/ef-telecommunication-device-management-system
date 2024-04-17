import Toast, { PluginOptions, POSITION } from 'vue-toastification';
import "vue-toastification/dist/index.css";

export const options: PluginOptions = {
    position: POSITION.BOTTOM_RIGHT,
    timeout: 5000,
}

export default Toast;