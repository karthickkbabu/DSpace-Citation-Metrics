/**
 * Functions to add citation count or other statistics from several
 * services (like Scopus) to the impact section of an item view.
 */

var IMPACT_SERVLET_URL = "/impact/ImpactServlet.py";

function addWebOfScienceCitationCount() {
    var doi = $("#wos").data("doi");
    $.getJSON(IMPACT_SERVLET_URL + "?service=wos&doi=" + doi)
        .done(function(data) {
            var citations = data["citationCount"];
            var linkBack = data["linkBack"];
            if (citations && linkBack) {
                $("#wos a").attr("href", linkBack);
                $("#wos .citation-count").html(citations);
                $("#wos").removeClass("hidden");
            }
        })
        .fail(function(jqxhr, textStatus, error) {
            console.log("Error retrieving Web of Science citation count: " + error);
        });
}

function addScopusCitationCount() {
    var doi = $("#scopus").data("doi");
    $.getJSON(IMPACT_SERVLET_URL + "?service=scopus&doi=" + doi)
        .done(function(data) {
            if (data["search-results"]["entry"]["0"]["@_fa"] === "not_true")
                return;

            var citations = data["search-results"]["entry"]["0"]["citedby-count"];
            var linkBack = getScopusLinkBack(data);

            if (citations > 0) {
                $("#scopus a").attr("href", linkBack);
                $("#scopus .citedby-count").html(citations);
                $("#scopus").removeClass("hidden");
            }
        })
        .fail(function(jqxhr, textStatus, error) {
            console.log("Error retrieving Scopus citation count: " + error);
        });
}

function getScopusLinkBack(data) {
    var linkList = data["search-results"]["entry"]["0"]["link"];
    var linkBackObject = $.grep(linkList, function(linkObject) {
            return linkObject["@ref"] === "scopus-citedby";
        })[0];

    return linkBackObject["@href"];
}

function addCitationCounts() {
    addWebOfScienceCitationCount();
    addScopusCitationCount();
}

$(document).ready(addCitationCounts);
