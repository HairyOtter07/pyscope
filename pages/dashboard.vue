<template>
    <div
        class="flex flex-col w-full h-full min-h-screen bg-slate-900 text-white items-center justify-center"
    >
        <div
            class="flex flex-row w-full items-center justify-between bg-slate-800/50 py-4 px-6 border-b-slate-400 border-b"
        >
            <p>BetterScope</p>
            <div class="flex flex-row-reverse gap-2">
                <div
                    v-if="loading"
                    class="bg-slate-700 w-52 rounded-lg animate-pulse"
                ></div>
                <p
                    v-else
                    class="peer hover:underline hover:cursor-pointer"
                    @click="logOut"
                >
                    {{ userName }}
                </p>
                <p class="invisible peer-hover:visible text-slate-400">
                    (Log Out)
                </p>
            </div>
        </div>
        <div
            class="flex flex-row w-full max-w-6xl h-full items-start justify-center gap-4"
        >
            <div
                class="sticky top-0 flex flex-col h-screen items-start justify-center p-8 gap-2"
            >
                <h2 class="whitespace-nowrap text-xl">Filters</h2>
                <div class="flex flex-col items-start justify-center">
                    <h2 class="whitespace-nowrap text-lg">By Course:</h2>
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
                    <div
                        v-else
                        class="flex flex-col items-start justify-center"
                    >
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
                <div class="flex flex-col items-start justify-center">
                    <h2 class="whitespace-nowrap text-lg">
                        By Submission Status:
                    </h2>
                    <div
                        class="flex flex-row gap-2 items-center p-0.5"
                        v-for="type in submissionTypes"
                    >
                        <div class="relative size-5">
                            <input
                                type="checkbox"
                                class="peer size-5 appearance-none bg-slate-300 checked:bg-slate-500 hover:cursor-pointer rounded"
                                v-model="type.visible"
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
                        <p class="whitespace-nowrap">{{ type.display }}</p>
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
                <div
                    class="sticky top-0 flex flex-row w-full justify-start bg-slate-900 py-4"
                >
                    <div
                        v-for="tab in filterTabs"
                        class="py-1 px-4 rounded hover:cursor-pointer"
                        :class="
                            filterType === tab.id
                                ? 'bg-slate-500 text-white'
                                : 'text-slate-400'
                        "
                        @click="changeFilter(tab)"
                    >
                        {{ tab.label }}
                    </div>
                </div>
                <template v-for="assignment in sortedAssignments">
                    <AssignmentCard
                        v-if="
                            courses.find(
                                (course) => course.id === assignment.course_id,
                            ).visible &&
                            submissionTypes.find(
                                (type) =>
                                    type.id ===
                                    assignment.submission_status.type,
                            ).visible &&
                            assignmentFilter(assignment)
                        "
                        :title="assignment.title"
                        :course="
                            courses.find(
                                (course) => course.id === assignment.course_id,
                            ).title
                        "
                        :submissionStatus="
                            formatSubmissionStatus(assignment.submission_status)
                        "
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
import { ref, shallowRef } from "vue";

const userName = ref("");
const courses = ref([]);
const assignments = ref([]);
const sortedAssignments = computed(() => {
    return assignments.value.toSorted((a, b) => {
        if (!a.due_date && !b.due_date) return 0;

        if (a.due_date && !b.due_date) return -1;
        if (!a.due_date && b.due_date) return 1;

        const aDue = dayjs(a.due_date);
        const bDue = dayjs(b.due_date);

        if (aDue.isBefore(bDue)) return -1;
        if (aDue.isAfter(bDue)) return 1;

        if (!a.late_due_date && !b.late_due_date) return 0;

        if (a.late_due_date && !b.late_due_date) return 1;
        if (!a.late_due_date && b.late_due_date) return -1;

        const aLate = dayjs(a.late_due_date);
        const bLate = dayjs(b.late_due_date);

        if (aLate.isBefore(bLate)) return -1;
        if (aLate.isAfter(bLate)) return 1;

        return 0;
    });
});
const loading = ref(true);

const nextSevenDaysFilter = (assignment) =>
    assignment.due_date
        ? dayjs().isBefore(dayjs(assignment.due_date)) &&
          dayjs(assignment.due_date).isBefore(dayjs().add(1, "week"))
        : false;
const lateFilter = (assignment) =>
    assignment.due_date && assignment.late_due_date
        ? dayjs(assignment.due_date).isBefore(dayjs()) &&
          dayjs().isBefore(dayjs(assignment.late_due_date))
        : false;
const pastDueFilter = (assignment) =>
    assignment.due_date
        ? assignment.late_due_date
            ? dayjs(assignment.late_due_date).isBefore(dayjs())
            : dayjs(assignment.due_date).isBefore(dayjs())
        : false;

const assignmentFilter = shallowRef(() => true);
const filterType = ref("all");

const filterTabs = [
    { id: "all", label: "All assignments", filterFn: () => true },
    {
        id: "nextSeven",
        label: "Next seven days",
        filterFn: nextSevenDaysFilter,
    },
    { id: "late", label: "Late", filterFn: lateFilter },
    { id: "pastDue", label: "Past due", filterFn: pastDueFilter },
];

const changeFilter = (tab) => {
    filterType.value = tab.id;
    assignmentFilter.value = tab.filterFn;
};

const submissionTypes = ref([
    {
        id: "NO_SUBMISSION",
        display: "No Submission",
        visible: true,
    },
    {
        id: "SUBMITTED",
        display: "Submitted",
        visible: true,
    },
    {
        id: "UNGRADED",
        display: "Ungraded",
        visible: true,
    },
    {
        id: "GRADED",
        display: "Graded",
        visible: true,
    },
]);

const formatSubmissionStatus = (status) => {
    let displayString = submissionTypes.value.find(
        (type) => type.id === status.type,
    ).display;
    if (status.type === "GRADED")
        displayString += `: ${status.score} / ${status.max_score}`;
    return displayString;
};

const logOut = async () => {
    cookieJar.value = null;
    await navigateTo("/login", { external: true });
};

onMounted(async () => {
    try {
        const nameResponse = await $fetch(
            `${config.public.apiBaseUrl}/api/name`,
            {
                method: "GET",
                headers: {
                    "GS-Cookie-Jar": cookieJar.value,
                },
            },
        );
        if (nameResponse.cookie_jar) {
            cookieJar.value = nameResponse.cookie_jar;
        }
        userName.value = nameResponse.name;
        const courseIdsResponse = await $fetch(
            `${config.public.apiBaseUrl}/api/courses`,
            {
                method: "GET",
                headers: {
                    "GS-Cookie-Jar": cookieJar.value,
                },
            },
        );
        if (courseIdsResponse.cookie_jar) {
            cookieJar.value = courseIdsResponse.cookie_jar;
        }
        for (const courseId of courseIdsResponse.course_ids) {
            const courseResponse = await $fetch(
                `${config.public.apiBaseUrl}/api/courses/${courseId}`,
                {
                    method: "GET",
                    headers: {
                        "GS-Cookie-Jar": cookieJar.value,
                    },
                },
            );
            if (courseResponse.cookie_jar) {
                cookieJar.value = courseResponse.cookie_jar;
            }
            const course = courseResponse.course;
            course.visible = true;
            courses.value.push(course);
            assignments.value = assignments.value.concat(course.assignments);
        }
        loading.value = false;
    } catch (err) {
        console.log(err);
    }
});
</script>
