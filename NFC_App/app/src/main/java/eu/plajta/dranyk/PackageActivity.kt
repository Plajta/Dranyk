package eu.plajta.dranyk

import android.annotation.SuppressLint
import android.content.Intent
import android.nfc.NfcAdapter
import android.nfc.Tag
import android.os.Bundle
import android.widget.Button
import android.widget.EditText
import androidx.activity.enableEdgeToEdge
import androidx.appcompat.app.AppCompatActivity

class PackageActivity : AppCompatActivity(), NfcAdapter.ReaderCallback {
    private lateinit var nfcAdapter: NfcAdapter

    @SuppressLint("MissingInflatedId")
    private fun setActivityDefaultState(){
        setContentView(R.layout.activity_package)
        val buttonSubmit = findViewById<Button>(R.id.package_submit_button)
        val nameInput = findViewById<EditText>(R.id.patient_name)
        val id = intent.getStringExtra("id")
        val type = intent.getStringExtra("type")
        val name = intent.getStringExtra("name")
        buttonSubmit.setOnClickListener {
            val patientName = nameInput.text.toString()
            val newPackage = Package(id = id.toString(), type = type.toString(), packageName = name.toString(),  patientName = patientName)
            DeliveryData.packages.add(newPackage)
            val intent = Intent(this, ScanActivity::class.java)
            startActivity(intent)
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