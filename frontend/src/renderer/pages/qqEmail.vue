<template>
    <div class="app-div">
        <div class="app-div__container">
            <div class="app-div__title">
                <h2>简历投递工具</h2>
            </div>
            <div class="app-div__input">
                <WsInput v-model="chromeUrl" placeholder="输入chrome.exe文件地址" />
                <WsInput type="text" v-model="searchKeyUrl" placeholder="输入投递文件地址" />
                <WsInput type="text" v-model="fileUrl" placeholder="输入投递简历地址" />
            </div>
            <div class="app-div__buttons">
                <WsButton @click="start">开始投递</WsButton>
                <WsButton @click="stop">停止投递</WsButton>
            </div>
            <div id="output">
                <b>输出：</b>
                {{ result }}
            </div>
        </div>

    </div>
</template>

<script setup>
import WsButton from "@/components/WsButton/index.vue";
import WsInput from "@/components/WsInput/index.vue";
import { ref } from "vue";

const result = ref("");
const chromeUrl = ref("");
const searchKeyUrl = ref("");
const fileUrl = ref("");
async function start() {
    if (!chromeUrl.value || !searchKeyUrl.value || !fileUrl.value) {
        window.alert("请填写完整信息");
        return;
    }
    try {
        const res = await fetch("http://127.0.0.1:8000/qq_email/start", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",  // 添加这行
            },
            body: JSON.stringify({
                chrome_driver_path: chromeUrl.value,
                search_file_path: searchKeyUrl.value,
                file_path: fileUrl.value,
            }),
        });
        const data = await res.json();
        result.value = JSON.stringify(data.message);
    } catch (e) {
        result.value = "请求失败: " + e.message;
    }
}

async function stop() {
    try {
        const res = await fetch("http://127.0.0.1:8000/qq_email/stop", {
            method: "POST",
        });
        const data = await res.json();
        result.value = JSON.stringify(data.message);
    } catch (e) {
        result.value = "请求失败: " + e.message;
    }
}
</script>


<style lang="scss" scoped>
.app-div {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100vh;
    background: linear-gradient(135deg, #f5f0ff 0%, #e6d6ff 50%, #ffffff 100%);

    &__container {
        width: 700px;
        height: 500px;
        padding: 20px;
        background: white;
        border-radius: 10px;
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        display: flex;
        flex-direction: column;
        align-items: center;
    }

    &__buttons {
        display: flex;
        gap: 30px;
        margin-top: 30px;
    }

    #output {
        flex: 1;
        min-height: 0;
        overflow-y: auto;
        white-space: pre-wrap;
        word-wrap: break-word;
        box-sizing: border-box;
        margin-top: 30px;
        display: flex;
        flex-direction: column;
        width: 100%;
        padding: 0 20px;
    }
}
</style>