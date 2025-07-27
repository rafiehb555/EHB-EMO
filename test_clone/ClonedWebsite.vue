<template>
    <div class="cloned-website">
        <h1>Example Domain</h1>
        <p></p>

        <!-- Navigation -->
        <nav v-for="nav in navigation" :key="nav.id" :class="nav.class">
            <a v-for="link in nav.links" :key="link.href" :href="link.href">
                {{ link.text }}
            </a>
        </nav>

        <!-- Main Content -->
        <main>
            <p>This component was generated from: https://example.com</p>
        </main>
    </div>
</template>

<script>
export default {
    name: 'ClonedWebsite',
    data() {
        return {
            navigation: []
        };
    }
};
</script>

<style scoped>
/* Import the extracted styles */
@import './assets/css/extracted-styles.css';
</style>