package eu.plajta.dranyk
import android.util.Log
import io.github.agrevster.pocketbaseKotlin.PocketbaseClient
import io.ktor.http.URLProtocol
import kotlinx.serialization.Serializable
import io.github.agrevster.pocketbaseKotlin.models.Record
import kotlinx.serialization.encodeToString
import kotlinx.serialization.json.Json

@Serializable
data class PackagesRecord(
    val packageName: String,
    val patientName: String,
    val type: String,
    val droneId: String
): Record()

object PocketBaseRepository {
    val client = PocketbaseClient({
        protocol = URLProtocol.HTTP
        host = "localhost"
        port = 8090
    })

    suspend fun authenticateUser(email: String, password: String): String? {
        return try {
            val token = client.users.authWithPassword(email, password).token
            Log.d("PocketBase", "Token: $token")
            this.client.authStore.token = token
            token
        } catch (e: Exception) {
            Log.e("PocketBase", "Authentication failed", e)
            null
        }
    }

    // Corrected method to use serialization properly
    suspend fun createPackage(record: PackagesRecord) {
        try {
            // Serialize the record to JSON string
            val jsonString = Json.encodeToString(record)
            Log.d("DeliverActivity", "Sending JSON: $jsonString")
            val response = this.client.records.create<PackagesRecord>("packages", jsonString)
            Log.d("PocketBase", "Package created: $response")
        } catch (e: Exception) {
            Log.e("PocketBase", "Failed to create package", e)
        }
    }
}
