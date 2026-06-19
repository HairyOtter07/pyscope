<template>
    <div
        class="flex flex-col w-full h-full min-h-screen bg-slate-900 text-white items-center justify-center"
    >
        <div
            class="flex flex-row w-full max-w-6xl h-full items-start justify-center gap-4"
        >
            <div
                class="sticky top-0 flex flex-col h-screen items-start justify-center p-8"
            >
                <h2 class="whitespace-nowrap">All Assignments</h2>
                <h2 class="whitespace-nowrap">Filter by Course</h2>
            </div>
            <div
                v-if="loading"
                class="flex flex-col w-full h-full items-center justify-center gap-3 p-8"
            >
                <div
                    v-for="i in 5"
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
            courses.value.push(course);
        }
        loading.value = false;
    } catch (err) {
        console.log(err);
    }
});
</script>
