<template>
    <div
        class="flex flex-col w-full h-full min-h-screen bg-slate-900 text-white items-center justify-center"
    >
        <div
            class="flex flex-row w-full max-w-6xl h-full items-start justify-center gap-4"
        >
            <div
                class="sticky top-0 flex flex-col h-screen items-start justify-center p-8 gap-1"
            >
                <h2 class="whitespace-nowrap text-xl">Filter by Courses</h2>
                <div v-if="loading">
                    <div
                        v-for="i in 4"
                        class="flex flex-row gap-2 items-center p-0.5"
                    >
                        <input
                            type="checkbox"
                            class="size-5 appearance-none bg-slate-500 rounded"
                        />
                        <div
                            class="h-6 w-52 bg-slate-800 animate-pulse rounded-md"
                        ></div>
                    </div>
                </div>
                <div v-else class="flex flex-col items-start justify-center">
                    <div
                        v-for="course in courses"
                        class="flex flex-row gap-2 items-center p-0.5"
                    >
                        <div class="relative size-5">
                            <input
                                type="checkbox"
                                class="peer size-5 appearance-none bg-slate-300 checked:bg-slate-500 hover:cursor-pointer rounded"
                                v-model="course.visible"
                            />
                            <svg
                                xmlns="http://www.w3.org/2000/svg"
                                width="20"
                                height="20"
                                viewBox="0 0 24 24"
                                class="invisible absolute inset-0 pointer-events-none peer-checked:visible"
                            >
                                <path d="M0 0h24v24H0z" fill="none" />
                                <path
                                    fill="currentColor"
                                    d="m9.55 15.15l8.475-8.475q.3-.3.7-.3t.7.3t.3.713t-.3.712l-9.175 9.2q-.3.3-.7.3t-.7-.3L4.55 13q-.3-.3-.288-.712t.313-.713t.713-.3t.712.3z"
                                />
                            </svg>
                        </div>
                        <p class="whitespace-nowrap">{{ course.title }}</p>
                    </div>
                </div>
            </div>
            <div
                v-if="loading"
                class="flex flex-col w-full h-full items-center justify-center gap-3 p-8"
            >
                <div
                    v-for="i in 8"
                    class="flex flex-row w-full items-center justify-between bg-slate-800 border-slate-400 rounded-lg p-4 animate-pulse"
                >
                    <div class="h-16"></div>
                </div>
            </div>
            <div
                v-else
                class="flex flex-col w-full h-full items-center justify-center gap-3 p-8"
            >
                <template v-for="course in courses">
                    <AssignmentCard
                        v-if="course.visible"
                        v-for="assignment in course.assignments"
                        :title="assignment.title"
                        :course="course.title"
                        :submissionStatus="assignment.submission_status"
                        :dueDate="
                            assignment.due_date
                                ? dayjs(assignment.due_date)
                                : undefined
                        "
                        :lateDueDate="
                            assignment.late_due_date
                                ? dayjs(assignment.late_due_date)
                                : undefined
                        "
                    />
                </template>
            </div>
        </div>
    </div>
</template>
<script setup>
useHead({
    title: "Dashboard",
});
const config = useRuntimeConfig();
const cookieJar = useCookie("gs_cookie_jar", { maxAge: 60 * 60 * 24 });
if (!cookieJar.value) {
    await navigateTo("/login", { external: true });
}

import dayjs from "dayjs";
import { ref } from "vue";

const courses = ref([]);
const loading = ref(true);

onMounted(async () => {
    try {
        const courseIds = await $fetch(
            `${config.public.apiBaseUrl}/api/courses`,
            {
                method: "GET",
                headers: {
                    "GS-Cookie-Jar": cookieJar.value,
                },
            },
        );
        for (const courseId of courseIds) {
            const course = await $fetch(
                `${config.public.apiBaseUrl}/api/courses/${courseId}`,
                {
                    method: "GET",
                    headers: {
                        "GS-Cookie-Jar": cookieJar.value,
                    },
                },
            );
            course.visible = true;
            courses.value.push(course);
        }
        loading.value = false;
    } catch (err) {
        console.log(err);
    }
});
</script>
