
package com.terousd.stream

import android.content.Context
import com.lagradost.cloudstream3.plugins.CloudstreamPlugin
import com.lagradost.cloudstream3.plugins.Plugin

@CloudstreamPlugin
class TerousdStreamPlugin : Plugin() {
    override fun load(context: Context) {
        registerMainAPI(TerousdStreamProvider())
    }
}
