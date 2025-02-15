package eu.plajta.dranyk

import android.annotation.SuppressLint
import android.content.Intent
import android.nfc.FormatException
import android.nfc.NfcAdapter
import android.nfc.Tag
import android.nfc.tech.Ndef
import android.os.Bundle
import android.util.Log
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
import java.io.IOException

class ScanActivity : AppCompatActivity(), NfcAdapter.ReaderCallback {

    private lateinit var nfcAdapter: NfcAdapter
    private lateinit var outputTextView: TextView

    @SuppressLint("SetTextI18n", "MissingInflatedId")
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_scan)

        outputTextView = findViewById(R.id.outputTextView)
        nfcAdapter = NfcAdapter.getDefaultAdapter(this)

        if (!nfcAdapter.isEnabled) {
            outputTextView.text = "NFC is disabled. Please enable NFC."
        } else {
            outputTextView.text = "NFC is enabled. Scan a tag."
        }
    }
    override fun onResume() {
        super.onResume()
        val options = Bundle()
        // Work around for some broken Nfc firmware implementations that poll the card too fast
        options.putInt(NfcAdapter.EXTRA_READER_PRESENCE_CHECK_DELAY, 250)

        // Enable ReaderMode for all types of card and disable platform sounds
        nfcAdapter.enableReaderMode(
            this,
            this,
            NfcAdapter.FLAG_READER_NFC_A or
                    NfcAdapter.FLAG_READER_NFC_B or
                    NfcAdapter.FLAG_READER_NFC_F or
                    NfcAdapter.FLAG_READER_NFC_V or
                    NfcAdapter.FLAG_READER_NFC_BARCODE,
            options
        )
    }

    override fun onPause() {
        super.onPause()
        val nfcAdapter = NfcAdapter.getDefaultAdapter(this)
        nfcAdapter.disableForegroundDispatch(this)
    }

    override fun onTagDiscovered(tag: Tag?) {
        val mNdef = Ndef.get(tag)
        if (mNdef != null) {
            try {
                mNdef.connect()
                if (mNdef.isConnected) {
                    val mNdefMessage = mNdef.ndefMessage
                    var id = ""
                    var type = ""
                    var name = ""
                    for ((recordCount, record) in mNdefMessage.records.withIndex()) {
                        val payload = record.payload
                        val payloadText = String(payload, charset("UTF-8"))
                        when(recordCount){
                            0 -> id = payloadText
                            1 -> type = payloadText
                            2 -> name = payloadText
                        }
                    }
                    if (type == "drone"){
                        Log.d("NFC", "Drone, ID: $id, Name: $name")
                        DeliveryData.droneId = id
                        DeliveryData.droneName = name
                        val intent = Intent(this, DeliverActivity::class.java)
                        startActivity(intent)
                    }
                    else{
                        val intent = Intent(this, PackageActivity::class.java)
                        intent.putExtra("id", id)
                        intent.putExtra("type", type)
                        intent.putExtra("name", name)
                        startActivity(intent)
                    }


                }
            } catch (e: IOException) {
                e.printStackTrace()
            } catch (e: FormatException) {
                e.printStackTrace()
            } finally {
                try {
                    mNdef.close()
                } catch (e: IOException) {
                    e.printStackTrace()
                }
            }
        }
    }
}