
package com.terousd.stream

import com.lagradost.cloudstream3.MainAPI
import com.lagradost.cloudstream3.SearchResponse
import com.lagradost.cloudstream3.TvType

class TerousdStreamProvider : MainAPI() {

    override var mainUrl = "https://stream.terousd.site"

    override var name = "Terousd Stream"

    override val lang = "en"

    override val supportedTypes = setOf(TvType.Movie)

    override suspend fun search(
        query: String
    ): List<SearchResponse> {
        // Website search integration will be added here.
        return emptyList()
    }
}
