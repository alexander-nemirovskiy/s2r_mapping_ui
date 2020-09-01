package com.example.jaxb.generated;

import java.math.BigDecimal;

public class FareAttribute {
	@XmlAttribute(name = "fare_id", required = true)
	private String fareId;
	@XmlAttribute(name = "price", required = true)
	private BigDecimal price;
	@XmlAttribute(name = "currency_type", required = true)
	private String currencyType;
	@XmlSchemaType(name = "unsignedByte")
	@XmlAttribute(name = "payment_method", required = true)
	private short paymentMethod;
	@XmlSchemaType(name = "unsignedByte")
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