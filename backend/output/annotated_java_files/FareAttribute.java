package com.example.jaxb.generated;

import java.math.BigDecimal;

public class FareAttribute {
	//@RdfsClass("gtfs:FareClass")
	@RdfProperty(propertyName = "gtfs:fareUrl")
	//@RdfsClass("gtfs:FareRule")
	@XmlAttribute(name = "fare_id", required = true)
	private String fareId;
	@XmlAttribute(name = "price", required = true)
	private BigDecimal price;
	@XmlAttribute(name = "currency_type", required = true)
	private String currencyType;
	@XmlSchemaType(name = "unsignedByte")
	@RdfProperty(propertyName = "gtfs:paymentMethod")
	//@RdfsClass("gtfs:PaymentMethod")
	@XmlAttribute(name = "payment_method", required = true)
	private short paymentMethod;
	@XmlSchemaType(name = "unsignedByte")
	//@RdfsClass("gtfs:TransfersAllowedType")
	//NotFound
	@RdfProperty(propertyName = "gtfs:minimumTransferTime")
	//NotFound
	//NotFound
	//NotFound
	@RdfProperty(propertyName = "gtfs:transfers")
	//NotFound
	//@RdfsClass("gtfs:TransferType")
	@RdfProperty(propertyName = "gtfs:transferExpiryTime")
	//NotFound
	//NotFound
	//@RdfsClass("gtfs:TransferRule")
	@RdfProperty(propertyName = "gtfs:transferType")
	//NotFound
	@XmlAttribute(name = "transfers")
	private Short transfers;
	@XmlSchemaType(name = "unsignedInt")
	@XmlAttribute(name = "transfer_duration")
	private Long transferDuration;

	public FareAttribute() {
	}

	public String getFareId() {
		return fareId;
	}

	public void setFareId(String fareId) {
		this.fareId = fareId;
	}

	public BigDecimal getPrice() {
		return price;
	}

	public void setPrice(BigDecimal price) {
		this.price = price;
	}

	public String getCurrencyType() {
		return currencyType;
	}

	public void setCurrencyType(String currencyType) {
		this.currencyType = currencyType;
	}

	public short getPaymentMethod() {
		return paymentMethod;
	}

	public void setPaymentMethod(short paymentMethod) {
		this.paymentMethod = paymentMethod;
	}

	public Short getTransfers() {
		return transfers;
	}

	public void setTransfers(Short transfers) {
		this.transfers = transfers;
	}

	public Long getTransferDuration() {
		return transferDuration;
	}

	public void setTransferDuration(Long transferDuration) {
		this.transferDuration = transferDuration;
	}
}