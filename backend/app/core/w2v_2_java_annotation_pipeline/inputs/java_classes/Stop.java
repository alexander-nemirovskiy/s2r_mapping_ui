package com.example.jaxb.generated;

import java.math.BigDecimal;

public class Stop {
	@XmlAttribute(name = "stop_id", required = true)
	private String stopId;
	@XmlAttribute(name = "stop_code")
	private String stopCode;
	@XmlAttribute(name = "stop_name", required = true)
	private String stopName;
	@XmlAttribute(name = "stop_desc")
	private String stopDesc;
	@XmlAttribute(name = "stop_lat", required = true)
	private BigDecimal stopLat;
	@XmlAttribute(name = "stop_lon", required = true)
	private BigDecimal stopLon;
	@XmlAttribute(name = "zone_id")
	private String zoneId;
	@XmlAttribute(name = "stop_url")
	private String stopUrl;
	@XmlSchemaType(name = "unsignedByte")
	@XmlAttribute(name = "location_type")
	private Short locationType;
	@XmlSchemaType(name = "unsignedByte")
	@XmlAttribute(name = "parent_station")
	private Short parentStation;
	@XmlAttribute(name = "stop_timezone")
	private String stopTimezone;
	@XmlSchemaType(name = "unsignedByte")
	@XmlAttribute(name = "wheelchair_boarding")
	private Short wheelchairBoarding;

	public Stop() {
	}

	public String getStopId() {
		return stopId;
	}

	public void setStopId(String stopId) {
		this.stopId = stopId;
	}

	public String getStopCode() {
		return stopCode;
	}

	public void setStopCode(String stopCode) {
		this.stopCode = stopCode;
	}

	public String getStopName() {
		return stopName;
	}

	public void setStopName(String stopName) {
		this.stopName = stopName;
	}

	public String getStopDesc() {
		return stopDesc;
	}

	public void setStopDesc(String stopDesc) {
		this.stopDesc = stopDesc;
	}

	public BigDecimal getStopLat() {
		return stopLat;
	}

	public void setStopLat(BigDecimal stopLat) {
		this.stopLat = stopLat;
	}

	public BigDecimal getStopLon() {
		return stopLon;
	}

	public void setStopLon(BigDecimal stopLon) {
		this.stopLon = stopLon;
	}

	public String getZoneId() {
		return zoneId;
	}

	public void setZoneId(String zoneId) {
		this.zoneId = zoneId;
	}

	public String getStopUrl() {
		return stopUrl;
	}

	public void setStopUrl(String stopUrl) {
		this.stopUrl = stopUrl;
	}

	public Short getLocationType() {
		return locationType;
	}

	public void setLocationType(Short locationType) {
		this.locationType = locationType;
	}

	public Short getParentStation() {
		return parentStation;
	}

	public void setParentStation(Short parentStation) {
		this.parentStation = parentStation;
	}

	public String getStopTimezone() {
		return stopTimezone;
	}

	public void setStopTimezone(String stopTimezone) {
		this.stopTimezone = stopTimezone;
	}

	public Short getWheelchairBoarding() {
		return wheelchairBoarding;
	}

	public void setWheelchairBoarding(Short wheelchairBoarding) {
		this.wheelchairBoarding = wheelchairBoarding;
	}
}