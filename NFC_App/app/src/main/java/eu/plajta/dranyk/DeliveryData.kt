package eu.plajta.dranyk

data class Package(
    val id: String = "",
    val type: String = "Unknown",
    val packageName: String = "",
    val patientName: String = ""
)

object DeliveryData {
    var droneId: String = ""
    var droneName: String = ""
    var packages: MutableList<Package> = mutableListOf()
}
