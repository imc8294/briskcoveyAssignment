class UtilsHelper:
    def check_required_fields(self, data, required_fields):
        """
        Check if all required fields are present in the data.
        """
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return {"error": f"Missing required fields: {', '.join(missing_fields)}"}
        return None
    
    def check_status_value(self, status, valid_statuses=['pending', 'in_progress']):
        """
        Check if the status value is valid.
        """
        if status.lower() not in valid_statuses:
            return {"error": f"Invalid status value: {status}. Valid values are: {', '.join(valid_statuses)}"}
        return None
    
    def error_msg_of_data(self, feild_name):
        """
        Check if the status value is valid.
        """
        return {"error": f"Please provide valid {feild_name} value"}