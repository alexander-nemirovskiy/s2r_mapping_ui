package com.example.jaxb.generated;

public class Agency {
	@XmlAttribute(name = "agency_id")
	private String agencyId;
	@XmlAttribute(name = "agency_name", required = true)
	private String agencyName;
	@XmlAttribute(name = "agency_url", required = true)
	private String agencyUrl;
	@XmlAttribute(name = "agency_timezone", required = true)
	private String agencyTimezone;
	@XmlAttribute(name = "agency_lang")
	private String agencyLang;
	@XmlAttribute(name = "agency_phone")
	private String agencyPhone;
	@XmlAttribute(name = "agency_fare_url")
	private String agencyFareUrl;

	public Agency() {
	}

	public String getAgencyId() {
		return agencyId;
	}

	public void setAgencyId(String agencyId) {
		this.agencyId = agencyId;
	}

	public String getAgencyName() {
		return agencyName;
	}

	public void setAgencyName(String agencyName) {
		this.agencyName = agencyName;
	}

	public String getAgencyUrl() {
		return agencyUrl;
	}

	public void setAgencyUrl(String agencyUrl) {
		this.agencyUrl = agencyUrl;
	}

	public String getAgencyTimezone() {
		return agencyTimezone;
	}

	public void setAgencyTimezone(String agencyTimezone) {
		this.agencyTimezone = agencyTimezone;
	}

	public String getAgencyLang() {
		return agencyLang;
	}

	public void setAgencyLang(String agencyLang) {
		this.agencyLang = agencyLang;
	}

	public String getAgencyPhone() {
		return agencyPhone;
	}

	public void setAgencyPhone(String agencyPhone) {
		this.agencyPhone = agencyPhone;
	}

	public String getAgencyFareUrl() {
		return agencyFareUrl;
	}

	public void setAgencyFareUrl(String agencyFareUrl) {
		this.agencyFareUrl = agencyFareUrl;
	}
}