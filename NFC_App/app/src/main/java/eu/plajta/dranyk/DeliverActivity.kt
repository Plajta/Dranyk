package eu.plajta.dranyk

import android.content.Intent
import android.nfc.NfcAdapter
import android.nfc.Tag
import android.os.Bundle
import android.util.Log
import android.widget.Button
import android.widget.Toast
import androidx.activity.enableEdgeToEdge
import androidx.appcompat.app.AppCompatActivity
import androidx.lifecycle.lifecycleScope

import kotlinx.coroutines.launch

class DeliverActivity : AppCompatActivity(), NfcAdapter.ReaderCallback {
    private lateinit var nfcAdapter: NfcAdapter

    private fun setActivityDefaultState(){
        setContentView(R.layout.activity_deliver)
        val buttonSubmit = findViewById<Button>(R.id.deliver_submit_button)
        buttonSubmit.setOnClickListener {
            val intent = Intent(this, MainActivity::class.java)
            startActivity(intent)
            Toast.makeText(this, "Successful Added", Toast.LENGTH_SHORT).show()
            for ( pack in DeliveryData.packages) {
                Log.d(
                    "NFC",
                    "ID: ${pack.id}, type: ${pack.type}, packageName: ${pack.packageName}, patientName: ${pack.patientName}"
                )
                val newPackage = PackagesRecord(
                    packageName = pack.packageName,
                    patientName = pack.patientName,
                    type = pack.type,
                    droneId = DeliveryData.droneId
                )

                // Call the createPackage function in a coroutine
                lifecycleScope.launch {
                    try {
                        PocketBaseRepository.createPackage(newPackage)
                        DeliveryData.droneId = ""
                        DeliveryData.droneName = ""
                        DeliveryData.packages.clear()
                    } catch (e: Exception) {
                        Log.e("DeliverActivity", "Error creating package", e)
                    }
                }
            }
        }
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setActivityDefaultState()
        enableEdgeToEdge()
        nfcAdapter = NfcAdapter.getDefaultAdapter(this)

    }
    override fun onResume() {
        super.onResume()
        setActivityDefaultState()
        val options = Bundle()
        options.putInt(NfcAdapter.EXTRA_READER_PRESENCE_CHECK_DELAY, 250)
        nfcAdapter.enableReaderMode(
            this,
            this,
            NfcAdapter.FLAG_READER_NFC_A or
                    NfcAdapter.FLAG_READER_NFC_B or
                    NfcAdapter.FLAG_READER_NFC_F or
                    NfcAdapter.FLAG_READER_NFC_V or
                    NfcAdapter.FLAG_READER_NFC_BARCODE or
                    NfcAdapter.FLAG_READER_NO_PLATFORM_SOUNDS,
            options
        )
    }
    override fun onTagDiscovered(tag: Tag?){

    }
}
