using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Web.Script.Serialization;
using System.Runtime.Caching;
using IBM.Data.DB2;
using CsvHelper;
using System.IO;
using System.Data;
using System.Data.OleDb;
using System.Globalization;

namespace DataApplication
{
    class Program
    {

        static void Main(string[] args)
        {

            //Visakan
            string MyDb2ConnectionString = "DATABASE=BLUDB;Server=dashdb-entry-yp-dal09-09.services.dal.bluemix.net:50000;UID=dash11634;PWD=sx_f8IBR8_wU;";

            //Nishanth
            //string MyDb2ConnectionString = "DATABASE=BLUDB;Server=dashdb-entry-yp-dal10-01.services.dal.bluemix.net:50000;UID=dash6242;PWD=C7yvzT_6h_UI;";

            DB2Connection MyDb2Connection = new DB2Connection(MyDb2ConnectionString);

            MyDb2Connection.Open();
            ReadCSVFile(MyDb2Connection);
            MyDb2Connection.Close();
            Console.ReadLine();
        }

        public static void ReadCSVFile(DB2Connection conn)
        {

            try
            {
                for (int i = 0; i < 53; i++)
                {
                    string filePath = @"G:\Dataset\language_filtered_reviews\english_reviews_";
                    filePath = filePath + i + ".csv";
                    if (!File.Exists(filePath))
                        break;

                    Console.WriteLine(i + " -Started");
                    DataTable dt = null;
                    bool fh = true;

                    dt = CsvFileToDatatable(filePath, fh);
                    PushToDatabase(dt, conn);
                    Console.WriteLine(i + " -Completed");
                }
            }
            catch (Exception)
            {

            }
        }


        public static void PushToDatabase(DataTable dt, DB2Connection conn)
        {
            try
            {

                using (DB2BulkCopy bulkCopy = new DB2BulkCopy(conn, DB2BulkCopyOptions.TableLock))
                {
                    bulkCopy.BulkCopyTimeout = 100000000;
                    // bulkCopy.NotifyAfter = 1000;
                    //bulkCopy.DB2RowsCopied += callme;
                    // bulkCopy.DestinationTableName = "DASH11634.NLP_YELP_REVIEWS";
                    bulkCopy.DestinationTableName = "NLP_LANGUAGE_FILTERED_REVIEWS";
                    bulkCopy.WriteToServer(dt);

                    foreach (var error in bulkCopy.Errors)
                    {
                        Console.WriteLine(error);
                    }
                }
            }
            catch (Exception ex)
            {

            }
        }


        public static DataTable CsvFileToDatatable(string path, bool IsFirstRowHeader)
        {
            string header = "No";
            string sql = string.Empty;
            DataTable dataTable = null;
            string pathOnly = string.Empty;
            string fileName = string.Empty;
            try
            {
                pathOnly = Path.GetDirectoryName(path);
                fileName = Path.GetFileName(path);
                sql = @"SELECT * FROM [" + fileName + "]";
                if (IsFirstRowHeader)
                {
                    header = "Yes";
                }
                using (OleDbConnection connection = new OleDbConnection(@"Provider=Microsoft.Jet.OLEDB.4.0;Data Source=" + pathOnly +
                ";Extended Properties=\"Text;HDR=" + header + "\""))
                {
                    using (OleDbCommand command = new OleDbCommand(sql, connection))
                    {
                        using (OleDbDataAdapter adapter = new OleDbDataAdapter(command))
                        {
                            dataTable = new DataTable();
                            dataTable.Locale = CultureInfo.CurrentCulture;
                            adapter.Fill(dataTable);
                        }
                    }
                }
            }
            catch (Exception ex)
            {

            }
            finally
            {
            }
            return dataTable;
        }



    }

    public static class DataTableExtensions
    {
        public static void WriteToCsvFile(this DataTable dataTable, string filePath)
        {
            StringBuilder fileContent = new StringBuilder();

            foreach (var col in dataTable.Columns)
            {
                fileContent.Append(col.ToString() + ",");
            }

            fileContent.Replace(",", System.Environment.NewLine, fileContent.Length - 1, 1);



            foreach (DataRow dr in dataTable.Rows)
            {

                foreach (var column in dr.ItemArray)
                {
                    fileContent.Append("\"" + column.ToString() + "\",");
                }

                fileContent.Replace(",", System.Environment.NewLine, fileContent.Length - 1, 1);
            }

            System.IO.File.WriteAllText(filePath, fileContent.ToString());

        }
    }
}


