<template>
    <div
        class="flex flex-col w-full h-full min-h-screen bg-slate-900 text-white items-center"
    >
        <div
            class="flex flex-col m-4 p-4 bg-slate-800 items-center justify-center border-white border rounded-md gap-2"
        >
            <h1 class="text-xl">Log In</h1>
            <form
                class="min-w-80 flex flex-col justify-center gap-4"
                @submit.prevent="login"
            >
                <div class="flex flex-col justify-center gap-2">
                    <div class="flex flex-col justify-center gap-1">
                        <label class="text-lg" for="email">Email:</label>
                        <input
                            class="p-2 bg-slate-700 border border-slate-400 rounded-md"
                            id="email"
                            type="text"
                            v-model="email"
                        />
                    </div>
                    <div class="flex flex-col justify-center gap-1">
                        <label class="text-lg" for="password">Password:</label>
                        <input
                            class="p-2 bg-slate-700 border border-slate-400 rounded-md"
                            id="password"
                            type="password"
                            v-model="password"
                        />
                    </div>
                </div>
                <div class="w-full">
                    <button
                        class="w-full p-2 bg-slate-700 border-slate-400 rounded-md hover:bg-slate-600 disabled:bg-zinc-600 disabled:text-zinc-300"
                        type="submit"
                        :disabled="loading"
                    >
                        {{ loading ? "Authenticating..." : "Log In" }}
                    </button>
                </div>
            </form>
            <div class="w-full text-green-300" v-if="success">
                <p>Success! Redirecting...</p>
            </div>
            <div class="w-full text-red-300" v-if="errorMessage">
                <p>{{ errorMessage }}</p>
            </div>
        </div>
    </div>
</template>
<script setup>
useHead({
    title: "Log In",
});
const config = useRuntimeConfig();

import { ref } from "vue";

const email = ref("");
const password = ref("");
const loading = ref(false);
const errorMessage = ref("");
const success = ref(false);
const cookieJar = useCookie("gs_cookie_jar", { maxAge: 60 * 60 * 24 });
if (cookieJar.value) {
    await navigateTo("/dashboard", { external: true });
}

const login = async () => {
    loading.value = true;
    success.value = false;
    errorMessage.value = "";

    try {
        const response = await $fetch(`${config.public.apiBaseUrl}/api/login`, {
            method: "POST",
            body: {
                email: email.value,
                password: password.value,
            },
        });

        if (response.cookie_jar) {
            success.value = true;
            cookieJar.value = response.cookie_jar;
            await navigateTo("/dashboard", { external: true });
        }
    } catch (err) {
        errorMessage.value =
            err.data?.detail ||
            "An unexpected error occurred. Please try again.";
    } finally {
        loading.value = false;
    }
};
</script>
