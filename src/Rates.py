from botocore.exceptions import ClientError
import logging
import os

logger = logging.getLogger(__name__)


class Rates:
    """Encapsulates an Amazon DynamoDB table of rates data."""

    def __init__(self, dyn_resource):
        """
        :param dyn_resource: A Boto3 DynamoDB resource.
        """
        self.dyn_resource = dyn_resource
        table_name = os.environ.get("DYNAMODB_TABLE", "exchange-local")
        self.table = self.dyn_resource.Table(table_name)

    def add_rates(self, rates):
        try:
            with self.table.batch_writer() as writer:
                for rate in rates:
                    writer.put_item(Item=rate)
                    print("Adding Rates:", rate)
        except ClientError as err:
            logger.error(
                f"Couldn't load data into table {self.table.name}. Here's why: {err.response['Error']['Code']}: {err.response['Error']['Message']}"
            )
            raise

    def get_rates(self, date):
        """
        Gets rates data from the table for a specific dates.
        :param date: datetime with format 2012-12-11/y-m-d
        :return: The data about the requested rates.
        """
        if type(date) is not str:
            date = str(date)
        try:
            response = self.table.get_item(Key={"time": date})
        except ClientError as err:
            logger.error(
                f"Couldn't get rates date= {date} from table {self.table.name}. Here's why: {err.response['Error']['Code']}: {err.response['Error']['Message']}"
            )
            raise
        else:
            return response.get("Item", [])
        pass
