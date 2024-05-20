using System;
using System.Collections.Generic;
using System.Linq;
using System.Net;
using Microsoft.Exchange.WebServices.Data;
using Newtonsoft.Json;

namespace OutlookLibraries
{
    public class EventInfo
    {
        public bool IsSendToAll { get; set; }
        public string EventId { get; set; }
        public string UID { get; set; }
        public string ChangeKey { get; set; }
        public string Subject { get; set; }
        public string Location { get; set; }
        public string Body { get; set; }
        public EmployeeInfo Organizer;
        public DateTime StartDate { get; set; }
        public DateTime FinishDate { get; set; }
        public List<EmployeeInfo> RequiredAttendee = null;
        public List<EmployeeInfo> OptionalAttendee = null;
    }

    public class MessageInfo
    {
        public string Body { get; set; }
        public string BodyType { get; set; }
        public string Subject { get; set; }
        public List<EmployeeInfo> Rerecipients = null;
        //Получатели в копии
        public List<EmployeeInfo> CcRerecipients = null;
        //Получатели в скрытой копии
        public List<EmployeeInfo> BcRerecipients = null;
    }

    public class AuthData
    {
        public string Login { get; set; }
        public string Password { get; set; }
    }
    public class EmployeeInfo
    {
        public string Email { get; set; }
        public string Status { get; set; }
    }
    public class ReturnData
    {
        public bool IsError;
        public string Message;
        public string EventId;
    }
    public class Program
    {
        public string Login { get; set; }
        public string Password { get; set; }
        public string ExchangeServer { get; set; }

        public Uri ExchangeUri()
        {
            //Uri uriEWS = new Uri("https://mail.tmk-group.com/EWS/Exchange.asmx");
            Uri uriEWS = new Uri(ExchangeServer);
            return uriEWS;
        }
        public static PropertySet EventProperties()
        {
            PropertySet EventProperties = new PropertySet(AppointmentSchema.Id, AppointmentSchema.ICalUid , AppointmentSchema.Subject, AppointmentSchema.Location, AppointmentSchema.Body, AppointmentSchema.Start, AppointmentSchema.End, AppointmentSchema.Organizer, AppointmentSchema.RequiredAttendees, AppointmentSchema.OptionalAttendees);
            return EventProperties;
        }


        public string GetLogin()
        {
            Console.WriteLine("login: " + Login);
            return Login;
        }
        public ExchangeService GetExchangeService()
        {
            ExchangeService service = new ExchangeService(ExchangeVersion.Exchange2013_SP1);
            Uri uriEWS = ExchangeUri();

            CredentialCache myCache = new CredentialCache();
            myCache.Add(uriEWS, "NTLM", new NetworkCredential(Login, Password));

            service.Credentials = myCache;
            service.Url = uriEWS;
            //service.TraceEnabled = true;
            //service.TraceFlags = TraceFlags.All;

            return service;
        }

        public string CreateMessage(string MessageParams)
        {
            bool IsError = false;
            string TextError = "";
            string sReturnData = "";
            string sBody = "";
            string sBodyType = "";
            string sSubject = "";
            string sRecipientEmail = "";
            ReturnData oReturnData = new ReturnData();
            List<EmployeeInfo> listRecipients = new List<EmployeeInfo>();
            List<EmployeeInfo> listCcRerecipients = new List<EmployeeInfo>();
            List<EmployeeInfo> listBcRerecipients = new List<EmployeeInfo>();

            try 
            {
                ExchangeService serviceEWS = GetExchangeService();
                EmailMessage emailMessage = new EmailMessage(serviceEWS);
                
                MessageInfo messageInfo = JsonConvert.DeserializeObject<MessageInfo>(MessageParams);
                sSubject = messageInfo.Subject;
                sBody = messageInfo.Body;
                sBodyType = messageInfo.BodyType;
                listRecipients = messageInfo.Rerecipients;
                listCcRerecipients = messageInfo.CcRerecipients;
                listBcRerecipients = messageInfo.BcRerecipients;

                emailMessage.Subject = sSubject;
                emailMessage.Body = sBody;
                if (sBodyType.ToLower() == "html")
                {
                    emailMessage.Body.BodyType = BodyType.HTML;
                }
                else
                {
                    emailMessage.Body.BodyType = BodyType.Text;
                }

                listRecipients = listRecipients ?? new List<EmployeeInfo>();
                listCcRerecipients = listCcRerecipients ?? new List<EmployeeInfo>();
                listBcRerecipients = listBcRerecipients ?? new List<EmployeeInfo>();

                foreach (EmployeeInfo employeeInfo in listRecipients){
                    sRecipientEmail = employeeInfo.Email;
                    if (sRecipientEmail != "")
                    {
                        emailMessage.ToRecipients.Add(sRecipientEmail);
                    }
                }

                foreach (EmployeeInfo employeeInfo in listCcRerecipients)
                {
                    sRecipientEmail = employeeInfo.Email;
                    if (sRecipientEmail != "")
                    {
                        emailMessage.CcRecipients.Add(sRecipientEmail);
                    }
                }

                emailMessage.SendAndSaveCopy();
            }
            catch (InvalidCastException e)
            {
                IsError = true;
                TextError = "В методе CreateMessage произошла ошибка: " + e.Message;
                Console.WriteLine(TextError);
            }

            catch (NullReferenceException e)
            {
                IsError = true;
                TextError = "В методе CreateMessage произошла ошибка: " + e.Message;
                Console.WriteLine(TextError);
            }

            catch (Newtonsoft.Json.JsonSerializationException e)
            {
                IsError = true;
                TextError = "В методе CreateMessage произошла ошибка при десериализации: " + e.Message;
                Console.WriteLine(TextError);
            }

            oReturnData.IsError = IsError;
            oReturnData.Message = TextError;
            sReturnData = JsonConvert.SerializeObject(oReturnData);
            return sReturnData;
        }

        public string CreateMeeting(string EventParams)
        {
            string sAttendeeAddress = "";
            List<EmployeeInfo> RequiredAttendee = new List<EmployeeInfo>();

            bool IsError = false;
            string TextError = "";
            string sReturnData = "";
            string EventId = "";
            ReturnData oReturnData = new ReturnData();

            try
            {
                string displayName = "Asia/Yekaterinburg";
                string standardName = "Ekaterinburg Standard Time";
                TimeSpan offset = new TimeSpan(05, 00, 00);
                TimeZoneInfo TimeZone = TimeZoneInfo.CreateCustomTimeZone(standardName, offset, displayName, standardName);
                TimeZoneInfo tz = TimeZoneInfo.FindSystemTimeZoneById("GMT Standard Time");

                EventInfo eventInfo = JsonConvert.DeserializeObject<EventInfo>(EventParams);
                string Subject = eventInfo.Subject;
                string Location = eventInfo.Location;
                string Body = eventInfo.Body;
                DateTime StartDate = eventInfo.StartDate;
                DateTime FinishDate = eventInfo.FinishDate;

                //Конвертим дату и время в GMT для совместимости с Outlook
                DateTime dtStart = TimeZoneInfo.ConvertTime(StartDate, tz);
                DateTime dtFinish = TimeZoneInfo.ConvertTime(FinishDate, tz);

                RequiredAttendee = eventInfo.RequiredAttendee;
                int iCountNewRequiredAttendees = RequiredAttendee.Count;

                ExchangeService serviceEWS = GetExchangeService();
                Appointment appointment = new Appointment(serviceEWS);

                appointment.Start = dtStart;
                appointment.End = dtFinish;
                appointment.StartTimeZone = TimeZone;
                appointment.EndTimeZone = TimeZone;
                appointment.Subject = Subject;
                appointment.Body = Body;
                appointment.Location = Location;

                for (int i = 0; i < iCountNewRequiredAttendees; i++)
                {
                    sAttendeeAddress = RequiredAttendee[i].Email;
                    if (sAttendeeAddress != "")
                    {
                        appointment.RequiredAttendees.Add(sAttendeeAddress);
                    }
                }

                appointment.Save(SendInvitationsMode.SendToAllAndSaveCopy);
                EventId = appointment.Id.ToString();
            }
            catch (InvalidCastException e)
            {
                IsError = true;
                TextError = "В методе CreateMeeting произошла ошибка: " + e.Message;
                Console.WriteLine(TextError);
            }
            catch (Newtonsoft.Json.JsonSerializationException e)
            {
                IsError = true;
                TextError = "В методе CreateMeeting произошла ошибка при десериализации списка сотрудников: " + e.Message;
                Console.WriteLine(TextError);
            }

            oReturnData.IsError = IsError;
            oReturnData.Message = TextError;
            oReturnData.EventId = EventId;
            sReturnData = JsonConvert.SerializeObject(oReturnData);
            return sReturnData;
        }
        public string UpdateMeeting(string EventParams)
        {
            bool IsSendToAll = false;
            string EventId = "";
            string Subject = "";
            string Location = "";
            string Body = "";
            string sAttendeeAddress = "";
            List<string> arrNewEmails = new List<string>();
            List<string> arrEventEmails = new List<string>();
            List<string> arrDelEmails = new List<string>();
            int iCountNewRequiredAttendees = 0;
            int iCountEventRequiredAttendees = 0;
            DateTime StartDate;
            DateTime FinishDate;
            List<EmployeeInfo> NewRequiredAttendee = new List<EmployeeInfo>();
            List<EmployeeInfo> LastRequiredAttendee = new List<EmployeeInfo>();

            string displayName = "Asia/Yekaterinburg";
            string standardName = "Ekaterinburg Standard Time";
            TimeSpan offset = new TimeSpan(05, 00, 00);
            TimeZoneInfo TimeZone = TimeZoneInfo.CreateCustomTimeZone(standardName, offset, displayName, standardName);
            TimeZoneInfo tz = TimeZoneInfo.FindSystemTimeZoneById("GMT Standard Time");

            bool IsError = false;
            string TextError = "";
            string sReturnData = "";
            ReturnData oReturnData = new ReturnData();

            try
            {
                EventInfo eventInfo = JsonConvert.DeserializeObject<EventInfo>(EventParams);
                EventId = eventInfo.EventId;
                IsSendToAll = eventInfo.IsSendToAll;
                Subject = eventInfo.Subject;
                Location = eventInfo.Location;
                Body = eventInfo.Body;
                StartDate = eventInfo.StartDate;
                FinishDate = eventInfo.FinishDate;
                NewRequiredAttendee = eventInfo.RequiredAttendee;
                iCountNewRequiredAttendees = NewRequiredAttendee.Count;

                //Конвертим дату и время в GMT для совместимости с Outlook
                DateTime dtStart = TimeZoneInfo.ConvertTime(StartDate, tz);
                DateTime dtFinish = TimeZoneInfo.ConvertTime(FinishDate, tz);

                ExchangeService serviceEWS = GetExchangeService();
                PropertySet Properties;
                Properties = EventProperties();
                Appointment appointment = Appointment.Bind(serviceEWS, EventId, new PropertySet(Properties));

                appointment.Subject = Subject;
                appointment.Location = Location;
                appointment.Start = dtStart;
                appointment.End = dtFinish;
                appointment.StartTimeZone = TimeZone;
                appointment.EndTimeZone = TimeZone;
                appointment.Body = Body;
                iCountEventRequiredAttendees = appointment.RequiredAttendees.Count;

                for (int i = 0; i < iCountNewRequiredAttendees; i++)
                {
                    sAttendeeAddress = NewRequiredAttendee[i].Email;
                    if (sAttendeeAddress != "")
                    {
                        arrNewEmails.Add(sAttendeeAddress);
                    }
                }

                for (int i = 0; i < iCountEventRequiredAttendees; i++)
                {
                    sAttendeeAddress = appointment.RequiredAttendees[i].Address;
                    if (sAttendeeAddress != "")
                    {
                        arrEventEmails.Add(sAttendeeAddress);
                    }
                }

                foreach (string employeeEmail in arrEventEmails)
                {
                    if (Array.IndexOf(arrNewEmails.ToArray(), employeeEmail) == -1)
                    {
                        arrDelEmails.Add(sAttendeeAddress);
                    }
                }

                foreach (string employeeEmail in arrNewEmails)
                {
                    if (Array.IndexOf(arrEventEmails.ToArray(), employeeEmail) == -1)
                    {
                        appointment.RequiredAttendees.Add(employeeEmail);
                    }
                }

                for (int i = 0; i < iCountEventRequiredAttendees; i++)
                {
                    sAttendeeAddress = appointment.RequiredAttendees[i].Address;
                    if (Array.IndexOf(arrDelEmails.ToArray(), sAttendeeAddress) != -1)
                    {
                        appointment.RequiredAttendees.RemoveAt(i);
                    }
                }

                if (IsSendToAll)
                {
                    appointment.Update(ConflictResolutionMode.AlwaysOverwrite, SendInvitationsOrCancellationsMode.SendOnlyToAll);
                }
                else
                {
                    appointment.Update(ConflictResolutionMode.AlwaysOverwrite, SendInvitationsOrCancellationsMode.SendOnlyToChanged);
                }
            }
            catch (InvalidCastException e)
            {
                IsError = true;
                TextError = "В методе UpdateMeeting произошла ошибка: " + e.Message;
            }
            catch (Newtonsoft.Json.JsonSerializationException e)
            {
                IsError = true;
                TextError = "В методе UpdateMeeting произошла ошибка при десериализации списка сотрудников: " + e.Message;
            }
            oReturnData.IsError = IsError;
            oReturnData.Message = TextError;
            sReturnData = JsonConvert.SerializeObject(oReturnData);
            return sReturnData;
        }
        public void CancelEvent(string EventId)
        {
            ExchangeService serviceEWS = GetExchangeService();
            Appointment appointment = Appointment.Bind(serviceEWS, new ItemId(EventId));
            appointment.Delete(DeleteMode.MoveToDeletedItems);
        }
        public string GetEventInfoById(string id)
        {
            //string sId = id;
            string EventId = id;
            string UID = "";
            string ChangeKey = "";
            string Location = "";
            string Body = "";
            string sAttendeeAddress = "";
            string sAttendeeStatus = "";
            string sReturnData = "";

            int iCountRequiredAttendees = 0;
            int iCountOptionalAttendees = 0;
            DateTime StartDate, FinishDate;
            EmployeeInfo Organizer;

            ExchangeService serviceEWS = GetExchangeService();
            Appointment meeting = Appointment.Bind(serviceEWS, new ItemId(EventId));

            EventInfo eventInfo = new EventInfo();
            Organizer = new EmployeeInfo();
            EventId = meeting.Id.ToString();
            UID = meeting.ICalUid.ToString();
            string Subject = meeting.Subject.ToString();
            Location = meeting.Location.ToString();
            Body = meeting.Body.ToString();
            StartDate = meeting.Start;
            FinishDate = meeting.End;
            Organizer.Email = meeting.Organizer.Address.ToString();

            iCountRequiredAttendees = meeting.RequiredAttendees.Count;
            iCountOptionalAttendees = meeting.OptionalAttendees.Count;

            List<EmployeeInfo> RequiredEmployeeInfo = new List<EmployeeInfo>();
            List<EmployeeInfo> OptionalEmployeeInfo = new List<EmployeeInfo>();
            for (int i = 0; i < iCountRequiredAttendees; i++)
            {
                sAttendeeAddress = meeting.RequiredAttendees[i].Address;
                sAttendeeStatus = meeting.RequiredAttendees[i].ResponseType.Value.ToString();
                RequiredEmployeeInfo.Add(new EmployeeInfo() { Email = sAttendeeAddress, Status = sAttendeeStatus });
            }

            for (int i = 0; i < iCountOptionalAttendees; i++)
            {
                sAttendeeAddress = meeting.OptionalAttendees[i].Address;
                sAttendeeStatus = meeting.OptionalAttendees[i].ResponseType.Value.ToString();
                OptionalEmployeeInfo.Add(new EmployeeInfo() { Email = sAttendeeAddress, Status = sAttendeeStatus });
            }

            eventInfo.EventId = EventId;
            eventInfo.UID = UID;
            eventInfo.Subject = Subject;
            eventInfo.Location = Location;
            eventInfo.Body = Body;
            eventInfo.StartDate = StartDate;
            eventInfo.FinishDate = FinishDate;
            eventInfo.Organizer = Organizer;
            eventInfo.RequiredAttendee = RequiredEmployeeInfo;
            eventInfo.OptionalAttendee = OptionalEmployeeInfo;

            sReturnData = JsonConvert.SerializeObject(eventInfo);
            return sReturnData;
        }
        public string GetEventInfoByDate(string EventParams)
        {
            string EventId = "";
            string UID = "";
            string ChangeKey = "";
            string Subject = "";
            string Location = "";
            string Body = "";
            string sAttendeeAddress = "";
            string sAttendeeStatus = "";
            string sReturnData = "";
            int iCountRequiredAttendees = 0;
            int iCountOptionalAttendees = 0;
            int iCountItems = 0;
            DateTime StartDate;
            DateTime FinishDate;
            EmployeeInfo Organizer;
            List<EventInfo> listEvents = new List<EventInfo>();
            PropertySet Properties;
            Properties = EventProperties();

            EventInfo eventInfo = JsonConvert.DeserializeObject<EventInfo>(EventParams);
            StartDate = eventInfo.StartDate;
            FinishDate = eventInfo.FinishDate;

            ExchangeService serviceEWS = GetExchangeService();
            // Initialize the calendar folder object with only the folder ID. 
            CalendarFolder calendar = CalendarFolder.Bind(serviceEWS, WellKnownFolderName.Calendar, new PropertySet());
            // Set the start and end time and number of appointments to retrieve.
            CalendarView cView = new CalendarView(StartDate, FinishDate);
            // Limit the properties returned to the appointment's subject, start time, and end time.
            cView.PropertySet = new PropertySet(BasePropertySet.IdOnly, AppointmentSchema.Start, AppointmentSchema.End);
            // Retrieve a collection of appointments by using the calendar view.
            FindItemsResults<Appointment> findResults = calendar.FindAppointments(cView);
            iCountItems = findResults.TotalCount;

            if (iCountItems > 0)
            {
                serviceEWS.LoadPropertiesForItems(from Item item in findResults select item, new PropertySet(Properties));

                foreach (Appointment a in findResults)
                {


                    eventInfo = new EventInfo();
                    Organizer = new EmployeeInfo();
                    EventId = a.Id.ToString();

                    if (a.ICalUid != null)
                    {
                        UID = a.ICalUid.ToString();
                    }
                    else
                    {
                        UID = "";
                    }

                    if (a.Subject != null)
                    {
                        Subject = a.Subject.ToString();
                    }
                    else
                    {
                        Subject = "";
                    }

                    if (a.Location != null)
                    {
                        Location = a.Location.ToString();
                    }
                    else
                    {
                        Location = "";
                    }

                    if (a.Body != null)
                    {
                        Body = a.Body.ToString();
                    }
                    else
                    {
                        Body = "";
                    }

                    StartDate = a.Start;
                    FinishDate = a.End;
                    Organizer.Email = a.Organizer.Address.ToString();

                    iCountRequiredAttendees = a.RequiredAttendees.Count;
                    iCountOptionalAttendees = a.OptionalAttendees.Count;

                    List<EmployeeInfo> RequiredEmployeeInfo = new List<EmployeeInfo>();
                    List<EmployeeInfo> OptionalEmployeeInfo = new List<EmployeeInfo>();
                    for (int i = 0; i < iCountRequiredAttendees; i++)
                    {
                        sAttendeeAddress = a.RequiredAttendees[i].Address;
                        sAttendeeStatus = a.RequiredAttendees[i].ResponseType.Value.ToString();
                        RequiredEmployeeInfo.Add(new EmployeeInfo() { Email = sAttendeeAddress, Status = sAttendeeStatus });
                    }

                    for (int i = 0; i < iCountOptionalAttendees; i++)
                    {
                        sAttendeeAddress = a.OptionalAttendees[i].Address;
                        sAttendeeStatus = a.OptionalAttendees[i].ResponseType.Value.ToString();
                        OptionalEmployeeInfo.Add(new EmployeeInfo() { Email = sAttendeeAddress, Status = sAttendeeStatus });
                    }

                    eventInfo.EventId = EventId;
                    eventInfo.UID = UID;
                    eventInfo.Subject = Subject;
                    eventInfo.Location = Location;
                    eventInfo.Body = Body;
                    eventInfo.StartDate = StartDate;
                    eventInfo.FinishDate = FinishDate;
                    eventInfo.Organizer = Organizer;
                    eventInfo.RequiredAttendee = RequiredEmployeeInfo;
                    eventInfo.OptionalAttendee = OptionalEmployeeInfo;
                    listEvents.Add(eventInfo);
                }
            }

            sReturnData = JsonConvert.SerializeObject(listEvents);
            return sReturnData;
        }
    }
}
