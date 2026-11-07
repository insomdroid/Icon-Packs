pluginManagement { repositories { google(); mavenCentral(); gradlePluginPortal() } }
dependencyResolutionManagement {
    repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS)
    repositories { google(); mavenCentral() }
}
rootProject.name = "InsomdroidIconPacks"
include(":app", ":core", ":pack-kitkat", ":pack-nothing", ":pack-holo", ":pack-material")
