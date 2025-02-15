package eu.plajta.dranyk

import android.content.Intent
import android.os.Bundle
import android.util.Log
import android.view.View
import android.widget.Button
import androidx.appcompat.app.AppCompatActivity
import androidx.lifecycle.lifecycleScope
import kotlinx.coroutines.launch

class MainActivity : AppCompatActivity() {

    private fun setActivityDefaultState(){
        setContentView(R.layout.activity_main)
        val buttonDelivery = findViewById<Button>(R.id.scan_start)
        val buttonLogin = findViewById<Button>(R.id.show_login)
        buttonDelivery.setOnClickListener {
            val intent = Intent(this, ScanActivity::class.java)
            startActivity(intent)
        }
        buttonLogin.setOnClickListener {
            val intent = Intent(this, LoginActivity::class.java)
            startActivity(intent)
        }
        val token = PocketBaseRepository.client.authStore.token
        Log.d("Main", "Token: $token")
        if (token != null) {
            buttonLogin.visibility = View.GONE
            buttonDelivery.visibility = View.VISIBLE
        } else {
            buttonLogin.visibility = View.VISIBLE
            buttonDelivery.visibility = View.GONE
        }
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setActivityDefaultState()
    }

    override fun onResume() {
        super.onResume()
        setActivityDefaultState()

    }
}
