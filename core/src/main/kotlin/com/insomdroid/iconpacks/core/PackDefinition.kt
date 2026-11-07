package com.insomdroid.iconpacks.core

data class PackDefinition(
    val id: String,
    val name: String,
    val applicationId: String,
    val description: String,
    val designDirection: String
)

object PackCatalog {
    val packs = listOf(
        PackDefinition("kitkat", "KitKat", "com.insomdroid.iconpacks.kitkat", "An original, faithful interpretation of Android 4.4 icon design.", "Soft dimensional forms, restrained gradients and KitKat-era proportions."),
        PackDefinition("nothing", "Nothing", "com.insomdroid.iconpacks.nothing", "An original geometric and dot-inspired icon language.", "Monochrome geometry, clear silhouettes and dot-based details."),
        PackDefinition("holo", "Holo", "com.insomdroid.iconpacks.holo", "An original interpretation of Android Holo-era visual design.", "Dark surfaces, crisp highlights and restrained cyan accents."),
        PackDefinition("material", "Material", "com.insomdroid.iconpacks.material", "An original interpretation of the original Material design era.", "Bold shapes, simple layers and confident color fields.")
    )
}
